// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: GameBalance.proto
// </auto-generated>
#pragma warning disable 1591, 0612, 3021
#region Designer generated code

using pb = global::Google.Protobuf;
using pbc = global::Google.Protobuf.Collections;
using pbr = global::Google.Protobuf.Reflection;
using scg = global::System.Collections.Generic;
namespace D3.GameBalance {

  /// <summary>Holder for reflection information generated from GameBalance.proto</summary>
  public static partial class GameBalanceReflection {

    #region Descriptor
    /// <summary>File descriptor for GameBalance.proto</summary>
    public static pbr::FileDescriptor Descriptor {
      get { return descriptor; }
    }
    private static pbr::FileDescriptor descriptor;

    static GameBalanceReflection() {
      byte[] descriptorData = global::System.Convert.FromBase64String(
          string.Concat(
            "ChFHYW1lQmFsYW5jZS5wcm90bxIORDMuR2FtZUJhbGFuY2UiMQoGSGFuZGxl",
            "EhkKEWdhbWVfYmFsYW5jZV90eXBlGAEgASgREgwKBGdiaWQYAiABKA8iXQoS",
            "Qml0UGFja2VkR2JpZEFycmF5EhAKCGVsZW1lbnRzGAEgAygPEhAKCGJpdGZp",
            "ZWxkGAIgASgMEiMKG2JpdGZpZWxkX2xlYWRpbmdfbnVsbF9ieXRlcxgDIAEo",
            "BWIGcHJvdG8z"));
      descriptor = pbr::FileDescriptor.FromGeneratedCode(descriptorData,
          new pbr::FileDescriptor[] { },
          new pbr::GeneratedClrTypeInfo(null, new pbr::GeneratedClrTypeInfo[] {
            new pbr::GeneratedClrTypeInfo(typeof(global::D3.GameBalance.Handle), global::D3.GameBalance.Handle.Parser, new[]{ "GameBalanceType", "Gbid" }, null, null, null),
            new pbr::GeneratedClrTypeInfo(typeof(global::D3.GameBalance.BitPackedGbidArray), global::D3.GameBalance.BitPackedGbidArray.Parser, new[]{ "Elements", "Bitfield", "BitfieldLeadingNullBytes" }, null, null, null)
          }));
    }
    #endregion

  }
  #region Messages
  public sealed partial class Handle : pb::IMessage<Handle> {
    private static readonly pb::MessageParser<Handle> _parser = new pb::MessageParser<Handle>(() => new Handle());
    private pb::UnknownFieldSet _unknownFields;
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public static pb::MessageParser<Handle> Parser { get { return _parser; } }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public static pbr::MessageDescriptor Descriptor {
      get { return global::D3.GameBalance.GameBalanceReflection.Descriptor.MessageTypes[0]; }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public Handle() {
      OnConstruction();
    }

    partial void OnConstruction();

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public Handle(Handle other) : this() {
      gameBalanceType_ = other.gameBalanceType_;
      gbid_ = other.gbid_;
      _unknownFields = pb::UnknownFieldSet.Clone(other._unknownFields);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public Handle Clone() {
      return new Handle(this);
    }

    /// <summary>Field number for the "game_balance_type" field.</summary>
    public const int GameBalanceTypeFieldNumber = 1;
    private int gameBalanceType_;
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int GameBalanceType {
      get { return gameBalanceType_; }
      set {
        gameBalanceType_ = value;
      }
    }

    /// <summary>Field number for the "gbid" field.</summary>
    public const int GbidFieldNumber = 2;
    private int gbid_;
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int Gbid {
      get { return gbid_; }
      set {
        gbid_ = value;
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override bool Equals(object other) {
      return Equals(other as Handle);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public bool Equals(Handle other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if (GameBalanceType != other.GameBalanceType) return false;
      if (Gbid != other.Gbid) return false;
      return Equals(_unknownFields, other._unknownFields);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override int GetHashCode() {
      int hash = 1;
      if (GameBalanceType != 0) hash ^= GameBalanceType.GetHashCode();
      if (Gbid != 0) hash ^= Gbid.GetHashCode();
      if (_unknownFields != null) {
        hash ^= _unknownFields.GetHashCode();
      }
      return hash;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void WriteTo(pb::CodedOutputStream output) {
      if (GameBalanceType != 0) {
        output.WriteRawTag(8);
        output.WriteSInt32(GameBalanceType);
      }
      if (Gbid != 0) {
        output.WriteRawTag(21);
        output.WriteSFixed32(Gbid);
      }
      if (_unknownFields != null) {
        _unknownFields.WriteTo(output);
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int CalculateSize() {
      int size = 0;
      if (GameBalanceType != 0) {
        size += 1 + pb::CodedOutputStream.ComputeSInt32Size(GameBalanceType);
      }
      if (Gbid != 0) {
        size += 1 + 4;
      }
      if (_unknownFields != null) {
        size += _unknownFields.CalculateSize();
      }
      return size;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void MergeFrom(Handle other) {
      if (other == null) {
        return;
      }
      if (other.GameBalanceType != 0) {
        GameBalanceType = other.GameBalanceType;
      }
      if (other.Gbid != 0) {
        Gbid = other.Gbid;
      }
      _unknownFields = pb::UnknownFieldSet.MergeFrom(_unknownFields, other._unknownFields);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            _unknownFields = pb::UnknownFieldSet.MergeFieldFrom(_unknownFields, input);
            break;
          case 8: {
            GameBalanceType = input.ReadSInt32();
            break;
          }
          case 21: {
            Gbid = input.ReadSFixed32();
            break;
          }
        }
      }
    }

  }

  public sealed partial class BitPackedGbidArray : pb::IMessage<BitPackedGbidArray> {
    private static readonly pb::MessageParser<BitPackedGbidArray> _parser = new pb::MessageParser<BitPackedGbidArray>(() => new BitPackedGbidArray());
    private pb::UnknownFieldSet _unknownFields;
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public static pb::MessageParser<BitPackedGbidArray> Parser { get { return _parser; } }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public static pbr::MessageDescriptor Descriptor {
      get { return global::D3.GameBalance.GameBalanceReflection.Descriptor.MessageTypes[1]; }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    pbr::MessageDescriptor pb::IMessage.Descriptor {
      get { return Descriptor; }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public BitPackedGbidArray() {
      OnConstruction();
    }

    partial void OnConstruction();

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public BitPackedGbidArray(BitPackedGbidArray other) : this() {
      elements_ = other.elements_.Clone();
      bitfield_ = other.bitfield_;
      bitfieldLeadingNullBytes_ = other.bitfieldLeadingNullBytes_;
      _unknownFields = pb::UnknownFieldSet.Clone(other._unknownFields);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public BitPackedGbidArray Clone() {
      return new BitPackedGbidArray(this);
    }

    /// <summary>Field number for the "elements" field.</summary>
    public const int ElementsFieldNumber = 1;
    private static readonly pb::FieldCodec<int> _repeated_elements_codec
        = pb::FieldCodec.ForSFixed32(10);
    private readonly pbc::RepeatedField<int> elements_ = new pbc::RepeatedField<int>();
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public pbc::RepeatedField<int> Elements {
      get { return elements_; }
    }

    /// <summary>Field number for the "bitfield" field.</summary>
    public const int BitfieldFieldNumber = 2;
    private pb::ByteString bitfield_ = pb::ByteString.Empty;
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public pb::ByteString Bitfield {
      get { return bitfield_; }
      set {
        bitfield_ = pb::ProtoPreconditions.CheckNotNull(value, "value");
      }
    }

    /// <summary>Field number for the "bitfield_leading_null_bytes" field.</summary>
    public const int BitfieldLeadingNullBytesFieldNumber = 3;
    private int bitfieldLeadingNullBytes_;
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int BitfieldLeadingNullBytes {
      get { return bitfieldLeadingNullBytes_; }
      set {
        bitfieldLeadingNullBytes_ = value;
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override bool Equals(object other) {
      return Equals(other as BitPackedGbidArray);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public bool Equals(BitPackedGbidArray other) {
      if (ReferenceEquals(other, null)) {
        return false;
      }
      if (ReferenceEquals(other, this)) {
        return true;
      }
      if(!elements_.Equals(other.elements_)) return false;
      if (Bitfield != other.Bitfield) return false;
      if (BitfieldLeadingNullBytes != other.BitfieldLeadingNullBytes) return false;
      return Equals(_unknownFields, other._unknownFields);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override int GetHashCode() {
      int hash = 1;
      hash ^= elements_.GetHashCode();
      if (Bitfield.Length != 0) hash ^= Bitfield.GetHashCode();
      if (BitfieldLeadingNullBytes != 0) hash ^= BitfieldLeadingNullBytes.GetHashCode();
      if (_unknownFields != null) {
        hash ^= _unknownFields.GetHashCode();
      }
      return hash;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public override string ToString() {
      return pb::JsonFormatter.ToDiagnosticString(this);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void WriteTo(pb::CodedOutputStream output) {
      elements_.WriteTo(output, _repeated_elements_codec);
      if (Bitfield.Length != 0) {
        output.WriteRawTag(18);
        output.WriteBytes(Bitfield);
      }
      if (BitfieldLeadingNullBytes != 0) {
        output.WriteRawTag(24);
        output.WriteInt32(BitfieldLeadingNullBytes);
      }
      if (_unknownFields != null) {
        _unknownFields.WriteTo(output);
      }
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public int CalculateSize() {
      int size = 0;
      size += elements_.CalculateSize(_repeated_elements_codec);
      if (Bitfield.Length != 0) {
        size += 1 + pb::CodedOutputStream.ComputeBytesSize(Bitfield);
      }
      if (BitfieldLeadingNullBytes != 0) {
        size += 1 + pb::CodedOutputStream.ComputeInt32Size(BitfieldLeadingNullBytes);
      }
      if (_unknownFields != null) {
        size += _unknownFields.CalculateSize();
      }
      return size;
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void MergeFrom(BitPackedGbidArray other) {
      if (other == null) {
        return;
      }
      elements_.Add(other.elements_);
      if (other.Bitfield.Length != 0) {
        Bitfield = other.Bitfield;
      }
      if (other.BitfieldLeadingNullBytes != 0) {
        BitfieldLeadingNullBytes = other.BitfieldLeadingNullBytes;
      }
      _unknownFields = pb::UnknownFieldSet.MergeFrom(_unknownFields, other._unknownFields);
    }

    [global::System.Diagnostics.DebuggerNonUserCodeAttribute]
    public void MergeFrom(pb::CodedInputStream input) {
      uint tag;
      while ((tag = input.ReadTag()) != 0) {
        switch(tag) {
          default:
            _unknownFields = pb::UnknownFieldSet.MergeFieldFrom(_unknownFields, input);
            break;
          case 10:
          case 13: {
            elements_.AddEntriesFrom(input, _repeated_elements_codec);
            break;
          }
          case 18: {
            Bitfield = input.ReadBytes();
            break;
          }
          case 24: {
            BitfieldLeadingNullBytes = input.ReadInt32();
            break;
          }
        }
      }
    }

  }

  #endregion

}

#endregion Designer generated code
